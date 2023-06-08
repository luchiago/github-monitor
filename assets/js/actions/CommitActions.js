import * as types from './ActionTypes';

export const createRepositorySuccess = (response, successMessage) => ({
  type: types.CREATE_REPOSITORY_SUCCESS,
  payload: { response, successMessage },
});

export const createRepositoryFailure = (errorMsg, successMessage) => ({
  type: types.CREATE_REPOSITORY_FAILURE,
  payload: { errorMsg, successMessage },
});

export const getCommitsSuccess = (commits) => ({
  type: types.GET_COMMITS_SUCCESS,
  payload: commits,
});
