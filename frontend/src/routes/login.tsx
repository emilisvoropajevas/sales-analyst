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

// Full Page centered container
// Cat Image
// White card (shadow, rounded corners)
    // Title
    // Username
    // Password
    // Log in Button 