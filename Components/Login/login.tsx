import { useForm } from "react-hook-form"
import axios from "axios";


function Login(){

    const {register,handleSubmit}=useForm();

 const onSubmit = async (data : any)=>{
 const response= await axios.get(
            "http://127.0.0.1:8000/workTracker/accounts/"
        );

        console.log(response.data);
 }
    return (
        <>
        <form onClick={handleSubmit(onSubmit)}>
            <label>Name:</label>
      <input
      {...register("Name")}
      />
      <label>Password</label>
      <input
       {...register("Password")} 
      />
      <button type={"submit"}>
      Login
      </button>
        </form>
        </>
    )
}

export default Login;