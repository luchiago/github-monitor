import React from 'react';
import { render } from '@testing-library/react';
import Form from './RepoCreateForm';
import { Provider } from 'react-redux';
import configureMockStore from 'redux-mock-store';

const mockStore = configureMockStore();
const store = mockStore({});
const mockGetElementById = jest.spyOn(document, 'getElementById');
const mockedUsername = 'mocked-username';
mockGetElementById.mockImplementation(() => ({
  dataset: {
    username: mockedUsername,
  },
}));

describe('RepoCreateForm component', () => {
  test('it renders correctly', () => {
    const handleSubmit = jest.fn();
    const props = {
      successMessage: false,
      handleSubmit,
      pristine: true,
      submitting: false,
      errorMsg: null,
    };
    const { getByPlaceholderText, queryByRole, container } = render(
      <Provider store={store}>
        <Form {...props} />
      </Provider>
    );

    expect(queryByRole('alert')).toBeFalsy();
    expect(getByPlaceholderText('Enter the repository name, must match {user}/{repo}')).toBeTruthy();
    expect(container.getElementsByClassName('form-control').length).toBe(1);
    expect(container.getElementsByClassName('invalid-feedback').length).toBe(0);
  });
});
