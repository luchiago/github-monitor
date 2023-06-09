/* eslint-disable react/prop-types */
import React from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import FilterButton from './FilterButton';

const Sidebar = (props) => {
  const { repositories } = props;

  return (
    <div id="sidebar-wrapper">
      <ul className="sidebar-nav">
        <li className="sidebar-brand">
          <Link to="/">Github Monitor</Link>
        </li>
        {repositories && repositories.map((name) => (
          <li key={name} className="sidebar-brand">
            <FilterButton query={name} type="repository__name" />
          </li>
        ))}
      </ul>
    </div>
  );
};

Sidebar.propTypes = {
  repositories: PropTypes.array,
};

const mapStateToProps = (store) => ({
  repositories: store.commitState.repositories,
});

export default connect(mapStateToProps)(Sidebar);
