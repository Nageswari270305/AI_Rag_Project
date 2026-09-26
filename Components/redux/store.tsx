import { configureStore } from "@reduxjs/toolkit";
import ProjectSlice from './projectSlice';

const store = configureStore({
    reducer : {
        project : ProjectSlice
    }
})
export default store;