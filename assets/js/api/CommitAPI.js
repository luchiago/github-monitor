import axios from 'axios';
import { reset } from 'redux-form';
import store from '../store';
import {
  createRepositorySuccess,
  createRepositoryFailure,
  getCommitsSuccess,
} from '../actions/CommitActions';

export const getCommits = async () => {
  const response = await axios.get('/api/commits/');
  const { results } = response.data;
  store.dispatch(getCommitsSuccess({ commits: results }));
};

export const createRepository = async (values, headers, formDispatch) => {
  try {
    const response = await axios.post('/api/repositories/', values, { headers });
    store.dispatch(createRepositorySuccess(response.data, true));
    formDispatch(reset('repoCreate'));
  } catch (error) {
    const errorData = error.response.data;
    const errorMsg = [];

    switch (error.response.status) {
      case 400: {
        // Validation Error
        const fieldNames = Object.keys(errorData);
        fieldNames.forEach((field) => {
          const message = errorData[field][0];
          const capitalized = message.charAt(0).toUpperCase() + message.slice(1);
          errorMsg.push(`${capitalized}`);
        });
        break;
      }
      case 404:
        // Not Found Repository
        errorMsg.push(`${errorData.message}`);
        break;
      default:
        errorMsg.push('Generic error');
    }
    store.dispatch(createRepositoryFailure(errorMsg, false));
    formDispatch(reset('repoCreate'));
  }
};
