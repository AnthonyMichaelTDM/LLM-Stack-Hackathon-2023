function SignUp() {
  return (
    <>
      <h1>Sign Up</h1>
      <form
        action={import.meta.env.VITE_API_URL + "/user/me/signup"}
        method="POST"
      >
        <label>
          Username
          <input type="text" name="username" />
        </label>
        <label>
          Password
          <input type="password" name="password" />
        </label>
        <label>
          Confirm Password
          <input type="password" name="confirmPassword" />
        </label>
        <button type="submit">Sign Up</button>
      </form>
    </>
  );
}

export default SignUp;
