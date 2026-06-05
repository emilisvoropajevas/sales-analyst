import { useMutation } from "@tanstack/react-query";
import { useNavigate } from "@tanstack/react-router";
import type { AxiosError } from "axios";
import { toast } from 'sonner'

import { 
    type BodyLoginAccessToken as AccessToken,
    Login,
    type Token,
} from "../client-axios";
import { extractErrorMessage } from "../utils";

const isLoggedIn = () => {
    return localStorage.getItem("access_token") !== null
}

const useAuth = () => {
    const navigate = useNavigate()

    const login = async (data: AccessToken) => {
        const response = await Login.loginAccessToken({
            body: data,
        })
        const token = response.data as Token
        localStorage.setItem("access_token", token.access_token)
    }

    const loginMutation = useMutation({
        mutationFn: login,
        onSuccess: () => {
            navigate({to: "/"})
        },
        onError: (err) => {
            toast.error(extractErrorMessage(err as AxiosError))
        }
    })

    const logout = () => {
        localStorage.removeItem("access_token")
        navigate({to: "/login"})
    }

    return {
        loginMutation,
        logout,
    }
}

export { isLoggedIn }
export default useAuth

