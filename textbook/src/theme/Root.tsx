import React, {useEffect} from 'react';
import type {ReactNode} from 'react';

export default function Root({children}: {children: ReactNode}): JSX.Element {
  useEffect(() => {
    const html = document.documentElement;
    const body = document.body;
    const isUrdu = html.getAttribute('lang')?.startsWith('ur');
    if (isUrdu) {
      body.classList.add('ur-body');
    } else {
      body.classList.remove('ur-body');
    }
  });

  return <>{children}</>;
}
