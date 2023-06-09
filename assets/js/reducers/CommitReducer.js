import * as types from '../actions/ActionTypes';

const initialState = {
  commits: [],
  successMessage: false,
  errorMsg: [],
  page: 1,
  nextPage: null,
  previousPage: null,
  repositories: [],
};

const commitReducer = (state = initialState, action) => {
  switch (action.type) {
    case types.GET_COMMITS_SUCCESS:
      return {
        ...state,
        commits: action.payload.commits,
        nextPage: action.payload.next,
        previousPage: action.payload.previous,
      };
    case types.CREATE_REPOSITORY_SUCCESS: {
      return {
        ...state,
        errorMsg: '',
        successMessage: action.payload.successMessage,
      };
    }
    case types.CREATE_REPOSITORY_FAILURE: {
      return {
        ...state,
        successMessage: action.payload.successMessage,
        errorMsg: action.payload.errorMsg,
      };
    }
    case types.GET_REPOSITORIES_SUCCESS: {
      return {
        ...state,
        repositories: action.payload.repositories,
      };
    }
    default:
      return state;
  }
};

export default commitReducer;
