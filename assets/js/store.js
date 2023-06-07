import { createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import reducers from './reducers/Index';

// Enable async/await with redux-thunk
const composedEnhancer = applyMiddleware(thunk);

const store = createStore(reducers, composedEnhancer);
export default store;
