import * as types from '../actions/ActionTypes';

const initialState = {
  commits: [],
  successMessage: false,
  errorMsg: '',
};

const commitReducer = (state = initialState, action) => {
  switch (action.type) {
    case types.GET_COMMITS_SUCCESS:
      return {
        ...state,
        commits: Object.values(action.payload),
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
    default:
      return state;
  }
};

export default commitReducer;
