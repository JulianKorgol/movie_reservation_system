'use client';

import { useState } from 'react';

import { useRouter } from 'next/navigation';

import { type LoginSchema, loginSchema } from '@/schemas/login.schema';
import { authService } from '@/services/auth.service';
import { zodResolver } from '@hookform/resolvers/zod';
import { AlertCircleIcon, Loader2Icon } from 'lucide-react';
import { useForm } from 'react-hook-form';
import { toast } from 'sonner';

import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export default function LoginForm({ onSwitchAction }: { onSwitchAction: () => void }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginSchema>({
    resolver: zodResolver(loginSchema),
    mode: 'onBlur',
  });

  const [serverErrors, setServerErrors] = useState<string[]>([]);
  const router = useRouter();

  const onSubmit = async (data: LoginSchema) => {
    setServerErrors([]);

    try {
      const response = await authService.login(data);

      localStorage.setItem('authToken', response.token);
      localStorage.setItem('authUser', JSON.stringify(response.account));

      toast.success(`Welcome back, ${response.account.firstName}!`);
      router.push('/');
    } catch (error) {
      toast.error('Login failed. Please check your credentials.');
      setServerErrors(['Invalid email or password.']);
    }
  };

  const allErrors = [
    ...Object.values(errors).map((err) => err?.message as string),
    ...serverErrors,
  ];

  return (
    <div className="font-sans min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <header>
        <h1 className="text-3xl font-bold text-center mt-10">Log In</h1>
      </header>

      <form
        onSubmit={handleSubmit(onSubmit)}
        className="flex flex-col gap-2 max-w-sm mx-auto mt-20"
        noValidate
      >
        <div>
          <label htmlFor="email" className="block text-sm font-medium mb-1">
            Email
          </label>
          <Input
            id="email"
            type="email"
            {...register('email')}
            className={errors.email ? 'border-red-500 focus:ring-red-500 focus:border-red-500' : ''}
          />
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium mb-1">
            Password
          </label>
          <Input
            id="password"
            type="password"
            {...register('password')}
            className={
              errors.password ? 'border-red-500 focus:ring-red-500 focus:border-red-500' : ''
            }
          />
        </div>

        <Button type="submit" className="w-full" disabled={isSubmitting}>
          {isSubmitting ? (
            <>
              <Loader2Icon className="animate-spin" />
              Logging In...
            </>
          ) : (
            'Log In'
          )}
        </Button>

        <Button type="button" variant="ghost" className="w-full mt-2" onClick={onSwitchAction}>
          Don&apos;t have an account? Sign Up
        </Button>

        {allErrors.length > 0 && (
          <Alert variant="destructive" className="mt-2 flex items-start gap-2">
            <AlertCircleIcon className="w-5 h-5 mt-1" />
            <div>
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>
                {allErrors.map((err, idx) => (
                  <span key={idx}>
                    {err}
                    <br />
                  </span>
                ))}
              </AlertDescription>
            </div>
          </Alert>
        )}
      </form>
    </div>
  );
}
