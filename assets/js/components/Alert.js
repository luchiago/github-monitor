/* eslint-disable react/prop-types */
import React from 'react';

const Alert = ({ alertTypeClass, message }) => (
  <>
    {message.map((msg) => (
      <div key={msg} className={`alert ${alertTypeClass}`} role="alert">
        {msg}
      </div>
    ))}
  </>
);

export default Alert;
