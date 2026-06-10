import { HttpClientTestingModule } from '@angular/common/http/testing';
import { provideZonelessChangeDetection } from '@angular/core';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { EtqPrintPage } from './etq-print.page';

describe('EtqPrintPage', () => {
  let fixture: ComponentFixture<EtqPrintPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EtqPrintPage, HttpClientTestingModule],
      providers: [provideZonelessChangeDetection()]
    }).compileComponents();

    fixture = TestBed.createComponent(EtqPrintPage);
  });

  it('should create', () => {
    expect(fixture.componentInstance).toBeTruthy();
  });
});
