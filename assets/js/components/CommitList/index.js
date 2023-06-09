import React from 'react';
import PropTypes from 'prop-types';
import validator from 'validator';
import { getCommits } from '../../api/CommitAPI';
import Pagination from '../Pagination';
import FilterButton from '../FilterButton';

const CommitList = (props) => {
  const changePage = (page) => {
    getCommits(page);
  };

  const { commits, previousPage, nextPage } = props;

  return (
    <div>
      {commits.length !== 0 && (
        <div>
          <div className="card card-outline-secondary my-4">
            <div className="card-header">
              Commit List
            </div>
            <Pagination
              changePage={changePage}
              previousPage={previousPage}
              nextPage={nextPage}
            />
            <div className="card-body">
              {commits.map((commit, index) => (
                <div key={commit.sha}>
                  <div className="avatar">
                    <img alt={commit.author} className="img-author" src={commit.avatar} />
                  </div>
                  <div className="commit-details">
                    <p>
                      {commit.message}
                    </p>
                    <small className="text-muted">
                      <FilterButton query={commit.author} type="author" />
                      {' '}
                      authored
                      {' '}
                      on
                      {' '}
                      <FilterButton query={commit.repository} type="repository__name" />
                      {' '}
                      at
                      {' '}
                      {commit.date}
                    </small>
                    {index !== commits.length - 1 && <hr />}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

CommitList.propTypes = {
  commits: PropTypes.arrayOf(PropTypes.object).isRequired,
  previousPage: PropTypes.string,
  nextPage: PropTypes.string,
};

export default CommitList;
