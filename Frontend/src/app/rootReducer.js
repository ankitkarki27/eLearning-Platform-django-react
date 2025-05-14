import { combineReducers } from '@reduxjs/toolkit';
import authReducer from '../features/authSlice';
import authApi from '@/features/api/authApi';

const rootReducer = combineReducers({
     [authApi.reducerPath]:authApi.reducer,
    
    auth: authReducer,

    // Add other reducers here as needed for course and all 
});

export default rootReducer;