const API_KEY = import.meta.env.VITE_API_KEY
const API_URL = import.meta.env.VITE_API_URL



export async function getSchedule() {
    const res = await fetch(`${API_URL}/api/v1/schedule?day_id=5&week_id=1&group_id=2`, {
        method: 'GET',
        headers: {
            'X-Api-Key': API_KEY
        }
    } )
    const jsonData = await res.json()
    return jsonData
}