/**
 * Next.js Middleware — Route Protection
 * Redirects unauthenticated users to /login
 * Redirects authenticated users away from auth pages
 */
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const PUBLIC_PATHS = ['/login', '/register'];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Check for token in cookies (server-side readable)
  const token = request.cookies.get('keeladi_token')?.value;

  const isPublicPath = PUBLIC_PATHS.some((p) => pathname.startsWith(p));
  const isRootPath = pathname === '/';

  // Redirect root to dashboard or login
  if (isRootPath) {
    return NextResponse.redirect(
      new URL(token ? '/dashboard' : '/login', request.url)
    );
  }

  // Redirect authenticated users away from auth pages
  if (isPublicPath && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  // Redirect unauthenticated users to login
  if (!isPublicPath && !token) {
    const loginUrl = new URL('/login', request.url);
    loginUrl.searchParams.set('redirect', pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico|icons|images).*)',
  ],
};
