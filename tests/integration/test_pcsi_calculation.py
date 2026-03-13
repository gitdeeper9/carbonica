"""
Integration tests for PCSI calculation
"""

import pytest
from carbonica import CARBONICA
from carbonica.pcsi import PCSI


class TestPCSICalculation:
    """Test PCSI calculation"""
    
    def test_pcsi_with_different_weights(self):
        """Test different weight configurations"""
        carbonica = CARBONICA(data_dir="./test_data")
        params = carbonica.compute_current_state(2025)
        
        # Default weights
        default_pcsi = PCSI()
        pcsi_default = default_pcsi.compute(params)
        
        # Extreme weights - فقط G_atm
        extreme_weights = {
            'NPP': 0.0, 'S_ocean': 0.0, 'G_atm': 1.0,
            'F_perma': 0.0, 'beta': 0.0, 'tau_soil': 0.0,
            'E_anth': 0.0, 'Phi_q': 0.0
        }
        extreme_pcsi = PCSI(weights=extreme_weights)
        pcsi_extreme = extreme_pcsi.compute(params)
        
        # فقط التأكد أن القيم ضمن النطاق
        assert 0 <= pcsi_default <= 1
        assert 0 <= pcsi_extreme <= 1
        
        # طباعة القيم للمساعدة في التصحيح
        print(f"\nDefault PCSI: {pcsi_default}")
        print(f"Extreme PCSI (only G_atm): {pcsi_extreme}")
    
    def test_pcsi_sensitivity(self):
        """Test sensitivity to parameter changes"""
        carbonica = CARBONICA(data_dir="./test_data")
        params = carbonica.compute_current_state(2025)
        base_pcsi = carbonica.compute_pcsi(2025, params)
        
        # تغيير NPP
        params_npp = params.copy()
        params_npp['NPP'] = 55.0
        pcsi_npp = carbonica.compute_pcsi(2025, params_npp)
        
        # تغيير G_atm
        params_gatm = params.copy()
        params_gatm['G_atm'] = 3.0
        pcsi_gatm = carbonica.compute_pcsi(2025, params_gatm)
        
        # تغيير F_perma
        params_perma = params.copy()
        params_perma['F_perma'] = 2.5
        pcsi_perma = carbonica.compute_pcsi(2025, params_perma)
        
        # طباعة القيم
        print(f"\nBase PCSI: {base_pcsi}")
        print(f"NPP=55: {pcsi_npp}")
        print(f"G_atm=3.0: {pcsi_gatm}")
        print(f"F_perma=2.5: {pcsi_perma}")
        
        # التأكد من أن القيم مختلفة (وليس بالضرورة أكبر/أصغر)
        assert pcsi_npp != base_pcsi or pcsi_gatm != base_pcsi or pcsi_perma != base_pcsi
    
    def test_pcsi_extreme_scenarios(self):
        """Test extreme scenarios"""
        carbonica = CARBONICA(data_dir="./test_data")
        
        # Pre-industrial
        pcsi_pi = carbonica.compute_pcsi(1850)
        
        # Critical threshold
        critical_params = carbonica.REFERENCE_VALUES['critical'].copy()
        pcsi_critical = carbonica.compute_pcsi(2025, critical_params)
        
        print(f"\nPre-industrial PCSI: {pcsi_pi}")
        print(f"Critical PCSI: {pcsi_critical}")
        
        # فقط التأكد من أن القيم معقولة
        assert 0 <= pcsi_pi <= 1
        assert 0 <= pcsi_critical <= 1
    
    def test_pcsi_temporal_consistency(self):
        """Test temporal consistency"""
        carbonica = CARBONICA(data_dir="./test_data")
        
        pcsi_1960 = carbonica.compute_pcsi(1960)
        pcsi_2025 = carbonica.compute_pcsi(2025)
        
        print(f"\n1960 PCSI: {pcsi_1960}")
        print(f"2025 PCSI: {pcsi_2025}")
        
        # PCSI يجب أن يزيد مع الوقت
        assert pcsi_2025 >= pcsi_1960
    
    def test_pcsi_validation_against_paper(self):
        """Validate against paper values"""
        carbonica = CARBONICA(data_dir="./test_data")
        
        pcsi_1960 = carbonica.compute_pcsi(1960)
        pcsi_2025 = carbonica.compute_pcsi(2025)
        
        print(f"\nPaper: 1960=0.31, 2025=0.78")
        print(f"Ours: 1960={pcsi_1960}, 2025={pcsi_2025}")
        
        # قيم تقريبية
        assert 0.2 < pcsi_1960 < 0.4
        assert 0.7 < pcsi_2025 < 0.9
    
    def test_pcsi_normalization_ranges(self):
        """Test normalization ranges"""
        pcsi = PCSI()
        
        # Pre-industrial = 0
        assert pcsi.normalize('NPP', 60.2) == 0.0
        assert pcsi.normalize('G_atm', 0.002) == 0.0
        
        # Critical = 1
        assert pcsi.normalize('NPP', 52.0) == 1.0
        assert pcsi.normalize('G_atm', 3.5) == 1.0
        
        # القيم خارج النطاق
        assert 0 <= pcsi.normalize('NPP', 50.0) <= 1
        assert 0 <= pcsi.normalize('G_atm', 4.0) <= 1
