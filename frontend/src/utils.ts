import { AxiosError } from "axios";

export function extractErrorMessage(err: AxiosError): string {
    const detail = (err.response?.data as any)?.detail

    if (Array.isArray(detail) && detail.length > 0) {
        return detail[0].msg
    }

    if (typeof detail == 'string') {
        return detail
    }

    return "Something went wrong"
}

export const getInitials = (name: string): string => {
    return name
        .split(" ")
        .slice(0, 2)
        .map((word) => word[0])
        .join("")
        .toUpperCase()
}