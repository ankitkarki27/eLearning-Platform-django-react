import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    isAuthenticated: false,
    user: null,
}

const authSlice= createSlice({
    name:"authSlice",
    initialState,

        reducers:{
            userLoggedIn:(state, action)=>{
                state.user = action.payload;
                state.isAuthenticated = true;
            }
        },
            userLoggedOut:(state)=>{
                state.user = null;
                state.isAuthenticated = false;
            },
});
export const { userLoggedIn, userLoggedOut } = authSlice.actions;
export default authSlice.reducer;
   
