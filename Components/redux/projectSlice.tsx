import { createSlice } from "@reduxjs/toolkit";
    const existing=JSON.parse(localStorage.getItem("Project")|| "[]");
  console.log(JSON.parse(localStorage.getItem("Project") || "[]"));
const ProjectSlice = createSlice({
    name:"project",
    initialState : {
        projects:existing
    },
    reducers:{
        addProject :(state,action)=>{
          localStorage.setItem("Project", JSON.stringify([...existing,action.payload]));
        //   console.log(JSON.parse(localStorage.getItem("Project") || "[]"));
        }
    }
})

export const { addProject } = ProjectSlice.actions;
export default ProjectSlice.reducer;