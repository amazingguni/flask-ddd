import sqlalchemy as sa
from sqlalchemy.ext import compiler
from sqlalchemy.schema import DDLElement, PrimaryKeyConstraint


class CreateView(DDLElement):
    def __init__(self, name, selectable, materialized=False):
        self.name = name
        self.selectable = selectable
        self.materialized = materialized


@compiler.compiles(CreateView)
def compile_create_materialized_view(element, compiler, **kw):
    return 'CREATE {}VIEW {} AS {}'.format(
        'MATERIALIZED ' if element.materialized else '',
        element.name,
        compiler.sql_compiler.process(element.selectable, literal_binds=True),
    )


class DropView(DDLElement):
    def __init__(self, name, materialized=False, cascade=True):
        self.name = name
        self.materialized = materialized
        self.cascade = cascade


@compiler.compiles(DropView)
def compile_drop_materialized_view(element, compiler, **kw):
    return 'DROP {}VIEW IF EXISTS {} {}'.format(
        'MATERIALIZED ' if element.materialized else '',
        element.name,
        'CASCADE' if element.cascade else ''
    )


def create_table_from_selectable(
    name,
    selectable,
    indexes=None,
    metadata=None,
    aliases=None
):
    if indexes is None:
        indexes = []
    if metadata is None:
        metadata = sa.MetaData()
    if aliases is None:
        aliases = {}
    args = [
        sa.Column(
            c.name,
            c.type,
            key=aliases.get(c.name, c.name),
            primary_key=c.primary_key
        )
        for c in selectable.c
    ] + indexes
    table = sa.Table(name, metadata, *args)

    if not any([c.primary_key for c in selectable.c]):
        table.append_constraint(
            PrimaryKeyConstraint(*[c.name for c in selectable.c])
        )
    return table


def create_materialized_view(
    name,
    selectable,
    metadata,
    indexes=None,
    aliases=None
):
    """ Create a view on a given metadata

    :param name: The name of the view to create.
    :param selectable: An SQLAlchemy selectable e.g. a select() statement.
    :param metadata:
        An SQLAlchemy Metadata instance that stores the features of the
        database being described.
    :param indexes: An optional list of SQLAlchemy Index instances.
    :param aliases:
        An optional dictionary containing with keys as column names and values
        as column aliases.

    Same as for ``create_view`` except that a ``CREATE MATERIALIZED VIEW``
    statement is emitted instead of a ``CREATE VIEW``.

    """
    table = create_table_from_selectable(
        name=name,
        selectable=selectable,
        indexes=indexes,
        metadata=None,
        aliases=aliases
    )

    sa.event.listen(
        metadata,
        'after_create',
        CreateView(name, selectable, materialized=True)
    )

    @sa.event.listens_for(metadata, 'after_create')
    def create_indexes(target, connection, **kw):
        for idx in table.indexes:
            idx.create(connection)

    sa.event.listen(
        metadata,
        'before_drop',
        DropView(name, materialized=True)
    )
    return table


def create_view(
    name,
    selectable,
    metadata,
    cascade_on_drop=True
):
    table = create_table_from_selectable(
        name=name,
        selectable=selectable,
        metadata=None
    )

    sa.event.listen(metadata, 'after_create', CreateView(name, selectable))

    @sa.event.listens_for(metadata, 'after_create')
    def create_indexes(target, connection, **kw):
        for idx in table.indexes:
            idx.create(connection)

    sa.event.listen(
        metadata,
        'before_drop',
        DropView(name, cascade=cascade_on_drop)
    )
    return table


def refresh_materialized_view(session, name, concurrently=False):
    session.flush()
    session.execute(
        'REFRESH MATERIALIZED VIEW {}{}'.format(
            'CONCURRENTLY ' if concurrently else '',
            name
        )
    )