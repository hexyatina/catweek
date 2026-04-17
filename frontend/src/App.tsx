import {useQuery} from "@tanstack/react-query";
import {getSchedule} from "./api.ts";

function App() {

    const {data} = useQuery({
        queryKey: ['schedule'],
        queryFn: () => getSchedule()
    })

  return (
    <>
        {JSON.stringify({data})}
    </>
  )
}

export default App
