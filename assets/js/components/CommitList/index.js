import React from 'react';
import { ArrowLeftSquareFill, ArrowRightSquareFill } from 'react-bootstrap-icons';
import PropTypes from 'prop-types';
import validator from 'validator';
import { filterCommits, getCommits } from '../../api/CommitAPI';

const NavButton = ({ disabled, onClick, action }) => (
  <>
    <button
      type="button"
      className="page-item btn-secondary"
      disabled={disabled}
      onClick={onClick}
    >
      {action === 'previous' ? <ArrowLeftSquareFill /> : <ArrowRightSquareFill />}
    </button>
  </>
);

const Pagination = ({ previousPage, nextPage }) => {
  const previousAction = (page) => {
    getCommits(page);
  };

  const nextAction = (page) => {
    getCommits(page);
  };

  return (
    <>
      <div className="pagination pagination-sm m-2">
        <NavButton
          disabled={previousPage === null}
          onClick={() => previousAction(previousPage)}
          action="previous"
        />
        <NavButton
          disabled={nextPage === null}
          onClick={() => nextAction(nextPage)}
          action="next"
        />
      </div>
    </>
  );
};

const CommitList = (props) => {
  const handleSearch = (query, type) => {
    const sanitizedInput = validator.escape(query);
    const searchParams = new URLSearchParams();
    searchParams.append(type, sanitizedInput);

    filterCommits(searchParams.toString());
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
            <Pagination previousPage={previousPage} nextPage={nextPage} />
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
                      <button className="btn btn-link button-link" type="reset" onClick={() => handleSearch(commit.author, 'author')}>
                        {commit.author}
                      </button>
                      {' '}
                      authored
                      {' '}
                      on
                      {' '}
                      <button className="btn btn-link button-link" type="reset" onClick={() => handleSearch(commit.repository, 'repository')}>
                        {commit.repository}
                      </button>
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
