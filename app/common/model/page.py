
class Page:
    page: int
    size: int
    total_count: int
    total_pages: int

    def __init__(self, page: int, size: int, total_count: int):
        self.page = page
        self.size = size
        self.total_count = total_count
        self.total_pages = self._calculate_total_pages()

    def _calculate_total_pages(self):
        total_pages = (int)(self.total_count / self.size)
        if self.total_count % self.size > 0:
            total_pages += 1
        return total_pages
