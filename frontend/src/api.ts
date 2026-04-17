const API_KEY = import.meta.env.VITE_API_KEY
const API_URL = import.meta.env.VITE_API_URL



export async function getSchedule() {
    const res = await fetch(`${API_URL}/schedule`, {
        method: 'GET',
        headers: {
            'X-Api-Key': API_KEY
        }
    } )
    console.log(API_KEY)

console.log(`${API_URL}/schedule`)
    const data = await res.json()
    return data
}