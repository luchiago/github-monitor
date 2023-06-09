import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import * as commitAPI from '../api/CommitAPI';
import Form from '../components/RepoCreateForm';

class RepoCreateContainer extends React.Component {
  submit = (values, dispatch) => {
    const token = document.getElementById('main').dataset.csrftoken;
    const name = values.name.split('/')[1];
    const v = { ...values, name };
    return commitAPI.createRepository(v, { 'X-CSRFToken': token }, dispatch);
  };

  render() {
    const { successMessage, errorMsg } = this.props;
    return <Form onSubmit={this.submit} successMessage={successMessage} errorMsg={errorMsg} />;
  }
}

RepoCreateContainer.propTypes = {
  successMessage: PropTypes.bool.isRequired,
  errorMsg: PropTypes.array
};

const mapStateToProps = (store) => ({
  successMessage: store.commitState.successMessage,
  errorMsg: store.commitState.errorMsg,
});

export default connect(mapStateToProps)(RepoCreateContainer);
