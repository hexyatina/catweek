// app/routes/app.tsx
import type { Route } from "./+types/app";

const apiURL = import.meta.env.VITE_API_URL;
const apiKey = import.meta.env.VITE_API_KEY;

console.log("Fetching:", `${apiURL}/api/v1/schedule`);
console.log("API key:", JSON.stringify(apiKey));

type ScheduleItem = {
  id: number;
  time: string;
  subject: string;
  room: string;
  instructor: string;
};

async function fetchSchedule(): Promise<ScheduleItem[]> {
  const response = await fetch(`${apiURL}/api/v1/schedule?detailed=true`, {
    headers: new Headers({
  "X-Api-Key": apiKey?.trim()
})
  });

  if (!response.ok) throw new Error("Failed to fetch schedule");
  return response.json();
}

export async function loader({}: Route.LoaderArgs) {
  const schedule = await fetchSchedule();
  return { schedule };
}

export function meta({}: Route.MetaArgs) {
  return [{ title: "Schedule" }];
}

export default function SchedulePage({ loaderData }: Route.ComponentProps) {
  return (
    <pre className="p-8 text-sm">
      {JSON.stringify(loaderData, null, 2)}
    </pre>
  );
}