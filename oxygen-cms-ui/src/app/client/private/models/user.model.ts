export interface User {
  id: string;
  isAdmin: boolean;
  email: string;
  password: string;
  confirmPassword: string;
  active: boolean;
  status: string;
  name: {
    first: string;
    last: string;
  };
}
