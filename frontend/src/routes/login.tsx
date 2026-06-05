import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/login")({
    loader: () => {
        return 'This is the login page'
    },
    component: Login,
})

function Login() {
    const data = Route.useLoaderData()
    return <div>{data}</div>
}