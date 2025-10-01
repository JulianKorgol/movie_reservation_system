'use client';

import { type SignUpSchema, signupSchema } from '@/schemas/signup.schema';
import { authService } from '@/services/auth.service';
import { zodResolver } from '@hookform/resolvers/zod';
import { AlertCircleIcon, Loader2Icon } from 'lucide-react';
import { useForm } from 'react-hook-form';
import { toast } from 'sonner';

import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export default function SignUpForm({ onSwitchAction }: { onSwitchAction: () => void }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<SignUpSchema>({
    resolver: zodResolver(signupSchema),
    mode: 'onBlur',
  });

  const onSubmit = async (data: SignUpSchema) => {
    try {
      const response = await authService.signUp(data);
      console.log('Sign-up response:', response);
      localStorage.setItem('authToken', response.token);
      toast.success(`Welcome, ${response.account.firstName}!`);
      await new Promise((resolve) => setTimeout(resolve, 1000));
      // TODO: redirect to dashboard
    } catch (error) {
      console.error('Sign-up failed:', error);
    }
  };

  const validationMessages = Object.values(errors)
    .map((err) => err.message)
    .filter(Boolean) as string[];

  return (
    <div className="font-sans min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <header>
        <h1 className="text-3xl font-bold text-center mt-10">Sign Up</h1>
      </header>

      <form
        onSubmit={handleSubmit(onSubmit)}
        className="flex flex-col gap-2 max-w-sm mx-auto mt-20"
        noValidate
      >
        <div className="flex gap-4">
          <div className="flex-1">
            <label htmlFor="firstName" className="block text-sm font-medium  mb-1">
              First Name
            </label>
            <Input
              id="firstName"
              {...register('firstName')}
              className={
                errors.firstName ? 'border-red-500 focus:ring-red-500 focus:border-red-500' : ''
              }
            />
          </div>
          <div className="flex-1">
            <label htmlFor="lastName" className="block text-sm font-medium  mb-1">
              Last Name
            </label>
            <Input
              id="lastName"
              {...register('lastName')}
              className={
                errors.lastName ? 'border-red-500 focus:ring-red-500 focus:border-red-500' : ''
              }
            />
          </div>
        </div>

        <div>
          <label htmlFor="email" className="block text-sm font-medium  mb-1">
            Email
          </label>
          <Input
            id="email"
            type="email"
            {...register('email')}
            className={errors.email ? 'border-red-500 focus:ring-red-500 focus:border-red-500' : ''}
          />
        </div>

        <div className="flex gap-4">
          <div className="flex-1">
            <label htmlFor="password" className="block text-sm font-medium  mb-1">
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
          <div className="flex-1">
            <label htmlFor="confirmPassword" className="block text-sm font-medium  mb-1">
              Confirm Password
            </label>
            <Input
              id="confirmPassword"
              type="password"
              {...register('confirmPassword')}
              className={
                errors.confirmPassword
                  ? 'border-red-500 focus:ring-red-500 focus:border-red-500'
                  : ''
              }
            />
          </div>
        </div>

        <Button type="submit" className="w-full" disabled={isSubmitting}>
          {isSubmitting ? (
            <>
              <Loader2Icon className="animate-spin" />
              Signing Up...
            </>
          ) : (
            'Sign Up'
          )}
        </Button>

        <Button type="button" variant="ghost" className="w-full mt-2" onClick={onSwitchAction}>
          Already have an account? Log In
        </Button>

        {validationMessages.length > 0 && (
          <Alert variant="destructive" className="mt-2 flex items-start gap-2">
            <AlertCircleIcon className="w-5 h-5 mt-1" />
            <div>
              <AlertTitle>Error</AlertTitle>
              <AlertDescription>
                {validationMessages.map((msg, idx) => (
                  <span key={idx}>
                    {msg}
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
