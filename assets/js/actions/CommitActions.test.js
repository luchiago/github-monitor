import * as actions from './CommitActions';
import * as types from './ActionTypes';

function randomBoolean() {
  return Math.random() < 0.5;
}

test('createRepositorySuccess returns type and payload with response and successMessage', () => {
  const response = {};
  const successMessage = randomBoolean();

  const result = actions.createRepositorySuccess(response, successMessage);

  expect(result.type).toBe(types.CREATE_REPOSITORY_SUCCESS);
  expect(result.payload.response).toBe(response);
  expect(result.payload.successMessage).toBe(successMessage);
});

test('createRepositoryFailure returns type and payload with errorMsg and successMessage', () => {
  const errorMsg = 'error';
  const successMessage = randomBoolean();

  const result = actions.createRepositoryFailure(errorMsg, successMessage);

  expect(result.type).toBe(types.CREATE_REPOSITORY_FAILURE);
  expect(result.payload.errorMsg).toBe(errorMsg);
  expect(result.payload.successMessage).toBe(successMessage);
});

test('getCommitsSuccess returns type and payload with commits', () => {
  const commits = [];

  const result = actions.getCommitsSuccess(commits);

  expect(result.type).toBe(types.GET_COMMITS_SUCCESS);
  expect(result.payload).toBe(commits);
});
