import React from 'react';
import { render } from '@testing-library/react';
import Alert from './Alert';

describe('Alert component', () => {
  test('it renders correctly', () => {
    const alertTypeClass = 'alert-success';
    const message = ['Test'];

    const { container, getByRole } = render(
      <Alert alertTypeClass={alertTypeClass} message={message} />,
    );

    expect(getByRole('alert')).toBeTruthy();
    expect(container.getElementsByClassName(alertTypeClass).length).toBe(1);
  });

  test('it renders multiple messages', () => {
    const alertTypeClass = 'alert-success';
    const message = ['Test', 'Test2'];

    const { container, getAllByRole } = render(
      <Alert alertTypeClass={alertTypeClass} message={message} />,
    );

    expect(getAllByRole('alert')).toBeTruthy();
    expect(container.getElementsByClassName(alertTypeClass).length).toBe(2);
  });

  test('it does not render without messages', () => {
    const alertTypeClass = 'alert-success';
    const message = [];

    const { queryByRole } = render(
      <Alert alertTypeClass={alertTypeClass} message={message} />,
    );

    expect(queryByRole('alert')).toBeFalsy();
  });
});
