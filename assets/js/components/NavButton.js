/* eslint-disable react/prop-types */
import React from 'react';
import { ArrowLeftSquareFill, ArrowRightSquareFill } from 'react-bootstrap-icons';

const NavButton = ({ disabled, onClick, action }) => (
  <>
    <button
      type="button"
      className="page-item btn-secondary"
      disabled={disabled}
      onClick={onClick}
    >
      {action === 'previous' ? <ArrowLeftSquareFill /> : <ArrowRightSquareFill />}
    </button>
  </>
);

export default NavButton;
