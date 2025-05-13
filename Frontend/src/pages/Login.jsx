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
import React, { useState } from 'react';

import {
    Tabs,
    TabsContent,
    TabsList,
    TabsTrigger,
} from "@/components/ui/tabs"

const Login = () => {

    // for the login and signup forms
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
        }
        else {
            setSignupInput((prev) => ({
                ...prev,
                [name]: value,
            }))
        }

    }
    return (
        <div className="flex items-center justify-center">
            <Tabs defaultValue="account" className="w-[400px]">
                <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="signup">Signup</TabsTrigger>
                    <TabsTrigger value="login">Login</TabsTrigger>
                </TabsList>
                <TabsContent value="signup">
                    <Card>
                        <CardHeader>
                            <CardTitle>Signup</CardTitle>
                            <CardDescription>
                                Create an account to start using our service.
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-2">
                            <div className="space-y-1">
                                <Label htmlFor="name">Name</Label>
                                <Input
                                    type="name"
                                    name="name"
                                    value={signupInput.name}
                                    id="name"
                                    onChange={(e) => changeInputHandler(e, "signup")}
                                    placeholder="John Doe"
                                    required="true" />
                            </div>
                            <div className="space-y-1">
                                <Label htmlFor="email">email</Label>
                                <Input
                                    type="email"
                                    name="email"
                                    value={signupInput.email}
                                    id="email"
                                      onChange={(e) => changeInputHandler(e, "signup")}
                                    placeholder="johndoe@gmail.com"
                                    required="true" />
                            </div>

                            <div className="space-y-1">
                                <Label htmlFor="password">password</Label>
                                <Input
                                    type="password"
                                    name="password"
                                    value={signupInput.password}
                                    id="password"
                                    onChange={(e) => changeInputHandler(e, "signup")}
                                    placeholder="Your password"
                                    required="true" />
                            </div>
                        </CardContent>
                        <CardFooter>
                            <Button>Signup</Button>
                        </CardFooter>
                    </Card>
                </TabsContent>
                <TabsContent value="login">
                    <Card>
                        <CardHeader>
                            <CardTitle>Login</CardTitle>
                            <CardDescription>
                                Login to your account to start using our service.
                            </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-2">
                            <div className="space-y-1">
                                <Label htmlFor="email">email</Label>
                                <Input
                                    type="email"
                                    name="email"
                                    value={loginInput.email}
                                    id="email"
                                    onChange={(e) => changeInputHandler(e, "login")}
                                    placeholder="johndoe@gmail.com"
                                    required="true" />
                            </div>

                            <div className="space-y-1">
                                <Label htmlFor="password">password</Label>
                                <Input
                                    type="password"
                                    name="password"
                                    value={loginInput.password}
                                    id="password"
                                    onChange={(e) => changeInputHandler(e, "login")}
                                    placeholder="Your password"
                                    required="true" />
                            </div>
                        </CardContent>
                        <CardFooter>
                            <Button>Login</Button>
                        </CardFooter>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    )
}

export default Login