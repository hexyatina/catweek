import {useQuery} from "@tanstack/react-query";
import {getSchedule} from "./api.ts";
import TableComponent from "./TableComponent.tsx";

function App() {

    const {data} = useQuery({
        queryKey: ['schedule'],
        queryFn: () => getSchedule()
    })

  return (
    <>
        <header className="content-center">
            <h1 className="justify-center">Table IPZ-32</h1>
        </header>
        <div>
            <TableComponent data={data} />
        </div>
    </>
  )
}

export default App
