import { useSelector} from "react-redux";

function Task(){
    const datas=useSelector((state : any)=>state.project.projects);
    console.log(datas,"datas");
      return (
        <>
            {datas.map((project : any) => (
                <div key={project.ProjectName}>
                    <p>Project Name: {project.ProjectName}</p>
                    <p>Project Handler: {project.ProjectHandler}</p>
                    <p>Project Status: {project.ProjectStatus}</p>
                </div>
            ))}
        </>
    );
}
export default Task;