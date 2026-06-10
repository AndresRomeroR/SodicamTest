import { Routes } from '@angular/router';
import { EtqPrintPage } from './pages/etq-print/etq-print.page';

export const routes: Routes = [
  { path: '', component: EtqPrintPage },
  { path: '**', redirectTo: '' }
];
