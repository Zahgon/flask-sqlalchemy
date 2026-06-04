from __future__ import annotations

import typing as t
from math import ceil

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
from flask import abort
from flask import request


class Pagination:
    """Apply an offset and limit to the query based on the current page and number of
    items per page.

    Don't create pagination objects manually. They are created by
    :meth:`.SQLAlchemy.paginate` and :meth:`.Query.paginate`.

    This is a base class, a subclass must implement :meth:`_query_items` and
    :meth:`_query_count`. Those methods will use arguments passed as ``kwargs`` to
    perform the queries.

    :param page: The current page, used to calculate the offset. Defaults to the
        ``page`` query arg during a request, or 1 otherwise.
    :param per_page: The maximum number of items on a page, used to calculate the
        offset and limit. Defaults to the ``per_page`` query arg during a request,
        or 20 otherwise.
    :param max_per_page: The maximum allowed value for ``per_page``, to limit a
        user-provided value. Use ``None`` for no limit. Defaults to 100.
    :param error_out: Abort with a ``404 Not Found`` error if no items are returned
        and ``page`` is not 1, or if ``page`` or ``per_page`` is less than 1, or if
        either are not ints.
    :param count: Calculate the total number of values by issuing an extra count
        query. For very complex queries this may be inaccurate or slow, so it can be
        disabled and set manually if necessary.
    :param kwargs: Information about the query to paginate. Different subclasses will
        require different arguments.

    .. versionchanged:: 3.0
        Iterating over a pagination object iterates over its items.

    .. versionchanged:: 3.0
        Creating instances manually is not a public API.
    """

    def __init__(
        self,
        page: int | None = None,
        per_page: int | None = None,
        max_per_page: int | None = 100,
        error_out: bool = True,
        count: bool = True,
        **kwargs: t.Any,
    ) -> None:
        self._query_args = kwargs
        page, per_page = self._prepare_page_args(
            page=page,
            per_page=per_page,
            max_per_page=max_per_page,
            error_out=error_out,
        )

        self.page: int = page
        """The current page."""

        self.per_page: int = per_page
        """The maximum number of items on a page."""

        self.max_per_page: int | None = max_per_page
        """The maximum allowed value for ``per_page``."""

        items = self._query_items()

        if not items and page != 1 and error_out:
            abort(404)

        self.items: list[t.Any] = items
        """The items on the current page. Iterating over the pagination object is
        equivalent to iterating over the items.
        """

        if count:
            total = self._query_count()
        else:
            total = None

        self.total: int | None = total
        """The total number of items across all pages."""


    @property
    def _query_offset(self) -> int:
        """The index of the first item to query, passed to ``offset()``.

        :meta private:

        .. versionadded:: 3.0
        """
        pass

    def _query_items(self) -> list[t.Any]:
        """Execute the query to get the items on the current page.

        Uses init arguments stored in :attr:`_query_args`.

        :meta private:

        .. versionadded:: 3.0
        """
        raise NotImplementedError

    def _query_count(self) -> int:
        """Execute the query to get the total number of items.

        Uses init arguments stored in :attr:`_query_args`.

        :meta private:

        .. versionadded:: 3.0
        """
        raise NotImplementedError

    @property
    def first(self) -> int:
        """The number of the first item on the page, starting from 1, or 0 if there are
        no items.

        .. versionadded:: 3.0
        """
        pass

    @property
    def last(self) -> int:
        """The number of the last item on the page, starting from 1, inclusive, or 0 if
        there are no items.

        .. versionadded:: 3.0
        """
        pass

    @property
    def pages(self) -> int:
        """The total number of pages."""
        pass

    @property
    def has_prev(self) -> bool:
        """``True`` if this is not the first page."""
        pass

    @property
    def prev_num(self) -> int | None:
        """The previous page number, or ``None`` if this is the first page."""
        pass

    def prev(self, *, error_out: bool = False) -> Pagination:
        """Query the :class:`Pagination` object for the previous page.

        :param error_out: Abort with a ``404 Not Found`` error if no items are returned
            and ``page`` is not 1, or if ``page`` or ``per_page`` is less than 1, or if
            either are not ints.
        """
        pass

    @property
    def has_next(self) -> bool:
        """``True`` if this is not the last page."""
        pass

    @property
    def next_num(self) -> int | None:
        """The next page number, or ``None`` if this is the last page."""
        pass

    def next(self, *, error_out: bool = False) -> Pagination:
        """Query the :class:`Pagination` object for the next page.

        :param error_out: Abort with a ``404 Not Found`` error if no items are returned
            and ``page`` is not 1, or if ``page`` or ``per_page`` is less than 1, or if
            either are not ints.
        """
        pass

    def iter_pages(
        self,
        *,
        left_edge: int = 2,
        left_current: int = 2,
        right_current: int = 4,
        right_edge: int = 2,
    ) -> t.Iterator[int | None]:
        """Yield page numbers for a pagination widget. Skipped pages between the edges
        and middle are represented by a ``None``.

        For example, if there are 20 pages and the current page is 7, the following
        values are yielded.

        .. code-block:: python

            1, 2, None, 5, 6, 7, 8, 9, 10, 11, None, 19, 20

        :param left_edge: How many pages to show from the first page.
        :param left_current: How many pages to show left of the current page.
        :param right_current: How many pages to show right of the current page.
        :param right_edge: How many pages to show from the last page.

        .. versionchanged:: 3.0
            Improved efficiency of calculating what to yield.

        .. versionchanged:: 3.0
            ``right_current`` boundary is inclusive.

        .. versionchanged:: 3.0
            All parameters are keyword-only.
        """
        pass

    def __iter__(self) -> t.Iterator[t.Any]:
        yield from self.items


class SelectPagination(Pagination):
    """Returned by :meth:`.SQLAlchemy.paginate`. Takes ``select`` and ``session``
    arguments in addition to the :class:`Pagination` arguments.

    .. versionadded:: 3.0
    """




class QueryPagination(Pagination):
    """Returned by :meth:`.Query.paginate`. Takes a ``query`` argument in addition to
    the :class:`Pagination` arguments.

    .. versionadded:: 3.0
    """


