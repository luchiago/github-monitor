import * as types from './ActionTypes';

export const createRepositorySuccess = (response, successMessage) => ({
  type: types.CREATE_REPOSITORY_SUCCESS,
  payload: { response, successMessage },
});

export const createRepositoryFailure = (errorMsg, successMessage) => ({
  type: types.CREATE_REPOSITORY_FAILURE,
  payload: { errorMsg, successMessage },
});

export const getCommitsSuccess = (commits, next, previous) => ({
  type: types.GET_COMMITS_SUCCESS,
  payload: { commits, next, previous },
});

export const getRepositoriesSuccess = (repositories) => ({
  type: types.GET_REPOSITORIES_SUCCESS,
  payload: { repositories },
});
