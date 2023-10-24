#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>
#include <utility>

#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include "TF1.h"
#include "TGraph.h"
#include "TCanvas.h"

struct Hit {
  double start;
  double end;
  double peakT;
  double TOT;
  double peakADC;
  double SADC;
};

std::vector<Hit> FindHits(const std::vector<double>& waveform, const double& thresh) {
  bool is_hit = false;

  std::vector<double> hit_charge;
  Hit this_hit;

  std::vector<Hit> hits;

  for (std::size_t tick = 0; tick < waveform.size(); ++tick) {
    double adc = waveform[tick];
    if (adc > thresh && !is_hit) {
      is_hit = true;
      this_hit.start = tick;
    }
    if (is_hit) {
      hit_charge.push_back(adc);
    }
    if (is_hit && adc < thresh) {
      this_hit.end = tick;
      is_hit = false;
      std::size_t peak_tick = std::distance(hit_charge.begin(), std::max_element(hit_charge.begin(), hit_charge.end()));
      this_hit.peakADC = hit_charge[peak_tick];
      this_hit.peakT = peak_tick;
      this_hit.SADC = std::accumulate(hit_charge.begin(), hit_charge.end(), 0.0);
      this_hit.TOT = this_hit.end - this_hit.start;
      hits.push_back(this_hit);
      // cleanup
      hit_charge.clear();
      this_hit = Hit();
    }
  }
  return hits;
}

int TPmaker() {
  TFile* file = new TFile("PedSubWaveform_Dump.root", "RECREATE");
  TTree* col_tree = new TTree("col_tree", "Collection waveforms");
  TTree* ind_tree = new TTree("ind_tree", "Induction waveforms");

  int event;
  int channel;
  std::vector<double>* waveform = nullptr;
  col_tree->Branch("event", &event);
  col_tree->Branch("channel", &channel);
  col_tree->Branch("waveform", &waveform);
  ind_tree->Branch("event", &event);
  ind_tree->Branch("channel", &channel);
  ind_tree->Branch("waveform", &waveform);

  std::ifstream col_file("PedSubWaveform_Dump.txt");
  std::string line;
  while (std::getline(col_file, line)) {
    std::istringstream iss(line);
    if (!(iss >> event >> channel)) { break; } // error
    waveform = new std::vector<double>;
    double adc;
    while (iss >> adc) {
      waveform->push_back(adc);
    }
    col_tree->Fill();
    delete waveform;
    waveform = nullptr;
  }
  col_file.close();

  std::ifstream ind_file("PedSubWaveformInd_Dump.txt");
  ind_tree->Branch("event", &event);
  ind_tree->Branch("channel", &channel);
  ind_tree->Branch("waveform", &waveform);
  while (std::getline(ind_file, line)) {
    std::istringstream iss(line);
    if (!(iss >> event >> channel)) { break; } // error
    waveform = new std::vector<double>;
    double adc;
    while (iss >> adc) {
      waveform->push_back(adc);
    }
    ind_tree->Fill();
    delete waveform;
    waveform = nullptr;
  }
  ind_file.close();

  file->Write();
  file->Close();

  TFile* infile = new TFile("PedSubWaveform_Dump.root");
  TTree* col_intree = (TTree*)infile->Get("col_tree");
  TTree* ind_intree = (TTree*)infile->Get("ind_tree");
  col_intree->SetBranchAddress("event", &event);
  col_intree->SetBranchAddress("channel", &channel);
  col_intree->SetBranchAddress("waveform", &waveform);
  ind_intree->SetBranchAddress("event", &event);
  ind_intree->SetBranchAddress("channel", &channel);
  ind_intree->SetBranchAddress("waveform", &waveform);

  TCanvas* col_canvas = new TCanvas("col_canvas", "Collection waveforms", 800, 600);
  col_canvas->Divide(5, 4);
  TCanvas* ind_canvas = new TCanvas("ind_canvas", "Induction waveforms", 800, 600);
  ind_canvas->Divide(5, 4);
  for (int i = 1; i <= 20; ++i) {
    col_intree->GetEntry(i - 1);
    std::cout << "Reading collection waveform for event " << event << ", channel " << channel << std::endl;

    waveform = nullptr;
    col_intree->SetBranchAddress("waveform", &waveform);
    col_intree->GetEntry(i - 1);

    if (waveform) {
      std::cout << "Collection waveform size: " << waveform->size() << std::endl;

      TH1F* hist = new TH1F(Form("col_hist_%d", i), Form("Collection waveform (event %d, channel %d)", event, channel), waveform->size(), 0, waveform->size());

      for (std::size_t j = 0; j < waveform->size(); ++j) {
        hist->SetBinContent(j + 1, (*waveform)[j]);
      }

      col_canvas->cd(i);
      hist->Draw();

      std::vector<Hit> hits = FindHits(*waveform, 30);
      for (const Hit& hit : hits) {
        hist->SetBinContent(hit.start + 1, hit.peakADC);
      }

      delete hist;
    } else {
      std::cout << "Error: No waveform data found." << std::endl;
    }

    delete waveform;
    waveform = nullptr;
  }
  col_canvas->Update();

  for (int i = 1; i <= 20; ++i) {
    ind_intree->GetEntry(i - 1);
    std::cout << "Reading induction waveform for event " << event << ", channel " << channel << std::endl;

    waveform = nullptr;
    ind_intree->SetBranchAddress("waveform", &waveform);
    ind_intree->GetEntry(i - 1);

    if (waveform) {
      std::cout << "Induction waveform size: " << waveform->size() << std::endl;

      TH1F* hist = new TH1F(Form("ind_hist_%d", i), Form("Induction waveform (event %d, channel %d)", event, channel), waveform->size(), 0, waveform->size());

      for (std::size_t j = 0; j < waveform->size(); ++j) {
        hist->SetBinContent(j + 1, (*waveform)[j]);
      }

      ind_canvas->cd(i);
      hist->Draw();
      delete hist;
    } else {
      std::cout << "Error: No waveform data found." << std::endl;
    }

    delete waveform;
    waveform = nullptr;
  }
  ind_canvas->Update();

  infile->Close();

  return 0;
}
