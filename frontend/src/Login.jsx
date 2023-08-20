function Login() {
  return (
    <>
      <h1>Login</h1>
      <form action={import.meta.env.VITE_API_URL + "/user/me/token"} method="POST">
        <label>
          Username
          <input type="text" name="username" />
        </label>
        <label>
          Password
          <input type="password" name="password" />
        </label>
        <button type="submit">Login</button>
      </form>
    </>
  );
}

export default Login;
