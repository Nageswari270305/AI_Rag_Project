import { useForm } from "react-hook-form";
import { useState } from "react";
import { useDispatch } from "react-redux";
import {addProject} from '../redux/projectSlice.js'
import DashBoard from "./Dashboard";

function AddProjects(){

    const {register, handleSubmit}=useForm();
    const [projectData,setProjectData]=useState(false);
    const dispatch=useDispatch();

    const onSubmit=(data:any)=>{
        dispatch(addProject(data));
        setProjectData(true);
    }

    if(projectData){
        return  <DashBoard />
    }

    return(
        <form onSubmit={handleSubmit(onSubmit)}>
            <div>
                <label>Project Name</label>
                <input
                {...register("ProjectName")}
                />

                <label>Project Handler</label>
                <input
                {...register("ProjectHandler")}
                />
                <label>Project Status</label>
                <input
                {...register("ProjectStatus")}
                />
            <button>
                Click To Proceed
            </button>
            </div>
        </form>
    )
}
export default AddProjects;