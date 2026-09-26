import { useState } from 'react';
import '../CSS/DashBoard.css' 
import AddProjects from './AddProjects.tsx'
import Task from './task.tsx'

function DashBoard(){
    const [displayNewProject,setDisplayNewProject]=useState (false);
    const [displayTaks,setDisplayTasks]=useState(false);
    const moveToAddingNewProject=()=>{
       setDisplayNewProject(true);
    }

    const showTasks=()=>{
       setDisplayTasks(true);
    }
    if(displayTaks){
        return <Task />
    }
    if(displayNewProject){
       return <AddProjects />
    }
    return(
        <>
        <h3>Task Board</h3>
        <div className="Taskstatus">
            <div onClick={()=>
                moveToAddingNewProject()
            }>
                <h3>New project</h3>
                </div> 
          <div onClick={showTasks}>
            <h4>Tasks</h4>
          </div>
            <h4>Completed tasks</h4>
            <h4>Pending tasks</h4>
            <h4>InProgress</h4>
        </div>
        </>
    )
}

export default DashBoard;