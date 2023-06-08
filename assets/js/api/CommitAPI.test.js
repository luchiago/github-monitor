import axios from 'axios';
import { reset } from 'redux-form';
import store from '../store';
import { getCommits, createRepository } from './CommitAPI';
import {
  createRepositorySuccess,
  createRepositoryFailure,
  getCommitsSuccess,
} from '../actions/CommitActions';

jest.mock('axios');

describe('getCommits', () => {
  test('retrieve commits and dispatch them', async () => {
    const mockResponse = { data: { commits: [1, 2, 3] } };
    axios.get.mockResolvedValue(mockResponse);
    const dispatchSpy = jest.spyOn(store, 'dispatch');

    await getCommits();

    expect(dispatchSpy).toHaveBeenCalledWith(getCommitsSuccess(mockResponse.data));
  });
});

describe('createRepository', () => {
  test('should create a repository', async () => {
    const mockValues = { name: 'test' };
    const mockHeaders = { Authorization: 'Bearer token' };
    const mockResponse = { data: { id: 1, name: 'test' } };

    axios.post.mockResolvedValue(mockResponse);

    const dispatchSpy = jest.spyOn(store, 'dispatch');
    const formDispatch = jest.fn();

    await createRepository(mockValues, mockHeaders, formDispatch);

    expect(dispatchSpy).toHaveBeenCalledWith(createRepositorySuccess(mockResponse.data, true));
    expect(formDispatch).toHaveBeenCalledWith(reset('repoCreate'));
  });

  test('should not create a repository on validation error', async () => {
    const mockValues = { name: 'invalid' };
    const mockHeaders = { Authorization: 'Bearer token' };
    const mockError = {
      response: {
        status: 400,
        data: { name: ['Name is required'] },
      },
    };
    axios.post.mockRejectedValue(mockError);
    const dispatchSpy = jest.spyOn(store, 'dispatch');
    const formDispatch = jest.fn();

    await createRepository(mockValues, mockHeaders, formDispatch);

    expect(dispatchSpy).toHaveBeenCalledWith(createRepositoryFailure(['Name is required'], false));
    expect(formDispatch).toHaveBeenCalledWith(reset('repoCreate'));
  });

  test('should not create a repository on not found error', async () => {
    const mockValues = { name: 'inexistent' };
    const mockHeaders = { Authorization: 'Bearer token' };
    const mockError = {
      response: {
        status: 404,
        data: { message: 'Not found repository' },
      },
    };
    axios.post.mockRejectedValue(mockError);
    const dispatchSpy = jest.spyOn(store, 'dispatch');
    const formDispatch = jest.fn();

    await createRepository(mockValues, mockHeaders, formDispatch);

    expect(dispatchSpy).toHaveBeenCalledWith(createRepositoryFailure(['Not found repository'], false));
    expect(formDispatch).toHaveBeenCalledWith(reset('repoCreate'));
  });

  test('should not create a repository on generic error', async () => {
    const mockValues = { name: 'generic' };
    const mockHeaders = { Authorization: 'Bearer token' };
    const mockError = {
      response: {
        status: 500,
        data: {},
      },
    };
    axios.post.mockRejectedValue(mockError);
    const dispatchSpy = jest.spyOn(store, 'dispatch');
    const formDispatch = jest.fn();

    await createRepository(mockValues, mockHeaders, formDispatch);

    expect(dispatchSpy).toHaveBeenCalledWith(createRepositoryFailure(['Generic error'], false));
    expect(formDispatch).toHaveBeenCalledWith(reset('repoCreate'));
  });
});
