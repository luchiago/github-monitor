/* eslint-disable react/prop-types */
import React from 'react';
import validator from 'validator';
import { filterCommits } from '../api/CommitAPI';

const FilterButton = ({ query, type }) => {
  const handleSearch = (paramQuery, paramType, dispatch) => {
    const sanitizedInput = validator.escape(paramQuery);
    const searchParams = new URLSearchParams();
    searchParams.append(paramType, sanitizedInput);

    filterCommits(searchParams.toString(), dispatch);
  };

  return (
    <button
      type="button"
      className="btn btn-link button-link"
      onClick={() => handleSearch(query, type)}
    >
      {query}
    </button>
  );
};

export default FilterButton;
