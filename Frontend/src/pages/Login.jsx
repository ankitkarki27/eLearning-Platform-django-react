import { Button } from "@/components/ui/button"
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import React, { useState } from 'react'

import {
    Tabs,
    TabsContent,
    TabsList,
    TabsTrigger,
} from "@/components/ui/tabs"

const Login = () => {

    const [loginInput, setLoginInput] = useState({
        email: "",
        password: "",
    })

    const [signupInput, setSignupInput] = useState({
        name: "",
        email: "",
        password: "",
    })

    const changeInputHandler = (e, type) => {
        const { name, value } = e.target;
        if (type === "login") {
            setLoginInput((prev) => ({
                ...prev,
                [name]: value,
            }))
        } else {
            setSignupInput((prev) => ({
                ...prev,
                [name]: value,
            }))
        }
    }

    return (
        <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-100 via-white to-gray-100 p-4">
            <Tabs defaultValue="signup" className="w-full max-w-md">
                <TabsList className="grid grid-cols-2 w-full mb-4 bg-gray-100 p- rounded-md shadow-inner">
                    <TabsTrigger value="signup" className="rounded-md">Signup</TabsTrigger>
                    <TabsTrigger value="login" className="rounded-md">Login</TabsTrigger>
                </TabsList>

                {/* Signup Form */}
                <TabsContent value="signup">
                    <Card className="shadow-lg rounded-xl border border-gray-200">
                        <CardHeader>
                            <CardTitle>Create Account</CardTitle>
                            <CardDescription>
                                Start your journey with us today.
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <Label htmlFor="name">Name</Label>
                                <Input
                                    id="name"
                                    name="name"
                                    type="text"
                                    placeholder="John Doe"
                                    value={signupInput.name}
                                    onChange={(e) => changeInputHandler(e, "signup")}
                                    required
                                />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="email">Email</Label>
                                <Input
                                    id="email"
                                    name="email"
                                    type="email"
                                    placeholder="johndoe@example.com"
                                    value={signupInput.email}
                                    onChange={(e) => changeInputHandler(e, "signup")}
                                    required
                                />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="password">Password</Label>
                                <Input
                                    id="password"
                                    name="password"
                                    type="password"
                                    placeholder="••••••••"
                                    value={signupInput.password}
                                    onChange={(e) => changeInputHandler(e, "signup")}
                                    required
                                />
                            </div>
                        </CardContent>
                        <CardFooter>
                            <Button className="w-full">Sign Up</Button>
                        </CardFooter>
                    </Card>
                </TabsContent>

                {/* Login Form */}
                <TabsContent value="login">
                    <Card className="shadow-lg rounded-xl border border-gray-200">
                        <CardHeader>
                            <CardTitle>Welcome Back</CardTitle>
                            <CardDescription>
                                Log in to continue to your dashboard.
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <Label htmlFor="email">Email</Label>
                                <Input
                                    id="email"
                                    name="email"
                                    type="email"
                                    placeholder="johndoe@example.com"
                                    value={loginInput.email}
                                    onChange={(e) => changeInputHandler(e, "login")}
                                    required
                                />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="password">Password</Label>
                                <Input
                                    id="password"
                                    name="password"
                                    type="password"
                                    placeholder="••••••••"
                                    value={loginInput.password}
                                    onChange={(e) => changeInputHandler(e, "login")}
                                    required
                                />
                            </div>
                        </CardContent>
                        <CardFooter>
                            <Button className="w-full">Log In</Button>
                        </CardFooter>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    )
}

export default Login
