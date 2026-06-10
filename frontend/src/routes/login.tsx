import { createFileRoute, redirect } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from 'sonner'

import catImage from "../assets/overlooking-cat.png"
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
// Add cat image above h2 tag later
    return (
        <div className="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
            
            <h2 className="mt-10 text-center text-2xl/9 font-bold tracking-tight text-black"> Sign in</h2>

            <div className="mt-10">
                <form className="space-y-6">
                    <div>
                        <label className="block text-sm/6 font-medium text-gray-700">Username</label>
                        <div className="mt-2">
                            <input id="username" type="text" name="username" required autoComplete="username" className="block w-full rounded-md bg-white/5 px-3 text-base text-black" />
                        </div>
                    </div>

                    <div className="flex items-center justify-between">
                        <label className="block font-medium text-gray-700">Password</label>

                        <div className="mt-2">
                            <input id="password" type="text" name="password" required autoComplete="username" className="block w-full rounded-md bg-white/5 px-3 text-base text-black" />
                        </div>
                    </div>
                    <div>
                        <button type="submit" className="flex w-full justify-center rounded-md bg-indigo-500 px-3 py-1.5">Log In</button>
                    </div>

                </form>

            </div>
        </div>
        

    )
}

// Full Page centered container
// Cat Image
// White card (shadow, rounded corners)
    // Title
    // Username
    // Password
    // Log in Button 