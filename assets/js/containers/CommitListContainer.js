import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import * as commitAPI from '../api/CommitAPI';
import CommitList from '../components/CommitList';

class CommitListContainer extends React.Component {
  componentDidMount() {
    commitAPI.getCommits();
    commitAPI.getRepositories();
  }

  render() {
    const { commits, previousPage, nextPage } = this.props;

    return (
      <div>
        <CommitList commits={commits} previousPage={previousPage} nextPage={nextPage} />
      </div>
    );
  }
}

CommitListContainer.propTypes = {
  commits: PropTypes.arrayOf(PropTypes.object).isRequired,
  previousPage: PropTypes.string,
  nextPage: PropTypes.string,
};

const mapStateToProps = (store) => ({
  commits: store.commitState.commits,
  previousPage: store.commitState.previousPage,
  nextPage: store.commitState.nextPage,
});

export default connect(mapStateToProps)(CommitListContainer);
