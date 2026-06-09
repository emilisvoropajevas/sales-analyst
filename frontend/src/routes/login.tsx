import { createFileRoute, redirect } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from 'sonner'
import useAuth, {isLoggedIn} from "../hooks/useAuth";

export const Route = createFileRoute("/login")({
    component: Login,
    beforeLoad: async () => {
        if (isLoggedIn()) {
            throw redirect({
                to: "/",
            })
        }
    },
    head: () => ({
        meta: [
            {
                title: "Log in - Product Analytics",
            },
        ],
    }),
})

function Login() {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const { loginMutation } = useAuth()

    const onSubmit = (e: React.SyntheticEvent<HTMLFormElement>) => {
        e.preventDefault()
        // Check for empty field names and return error
        if (!username.trim() || !password.trim()) {
            return toast.error("Field cannot be empty")
        }
        if (loginMutation.isPending) return
        loginMutation.mutate({ username, password })        
    }





}

// Full Page centered container
// Cat Image
// White card (shadow, rounded corners)
    // Title
    // Username
    // Password
    // Log in Button 