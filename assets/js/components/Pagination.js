/* eslint-disable react/prop-types */
import React from 'react';
import NavButton from './NavButton';

const Pagination = ({ changePage, previousPage, nextPage }) => (
  <div className="pagination pagination-sm m-2">
    <NavButton
      disabled={previousPage === null}
      onClick={() => changePage(previousPage)}
      action="previous"
    />
    <NavButton
      disabled={nextPage === null}
      onClick={() => changePage(nextPage)}
      action="next"
    />
  </div>
);

export default Pagination;
