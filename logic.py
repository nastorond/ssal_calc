# logic.py

def calculate_profits(inputs):
    """입력값을 받아 각 비약의 수익을 계산하고 결과를 반환합니다."""
    try:
        # 쉼표를 제거하고 숫자로 변환 (입력이 비어있으면 0으로 처리)
        oil = float(inputs["oil"].replace(",", "") or 0)
        item = float(inputs["item"].replace(",", "") or 0)
        stone = float(inputs["stone"].replace(",", "") or 0)
        celebration_price = float(inputs["celebration"].replace(",", "") or 0)
        recharge_price = float(inputs["recharge"].replace(",", "") or 0)
        small_recharge_price = float(inputs["small_recharge"].replace(",", "") or 0)

        # 각 비약의 재료비 계산
        base_cost = oil * 10 + item * 5 + stone * 2 + 1000
        base_cost2 = oil * 10 + item * 3 + stone * 1 + 1000
        base_cost3 = oil * 5 + item * 2 + stone * 1 + 1000

        # 각 비약별 수익 계산 (수수료 5% 차감)
        profit_celebration = (celebration_price * 3 - base_cost) * 100 * 0.95 if celebration_price > 0 else 0
        profit_recharge = (recharge_price * 3 - base_cost2) * 100 * 0.95 if recharge_price > 0 else 0
        profit_small_recharge = (small_recharge_price * 6 - base_cost3) * 100 * 0.95 if small_recharge_price > 0 else 0
        
        # 결과를 텍스트로 포맷팅
        result_text = (
            f"경축비 {profit_celebration:,.0f} 원\n"
            f"재획비 {profit_recharge:,.0f} 원\n"
            f"소형 재획비 {profit_small_recharge:,.0f} 원"
        )
        
        # [수정] 성공 시 글자색을 'black'으로 반환
        return result_text, "black"
        
    except (ValueError, TypeError):
        return "모든 칸에 숫자를 올바르게 입력해주세요.", "#FF4136" # 에러는 빨간색 유지
    except Exception as e:
        return f"알 수 없는 오류가 발생했습니다:\n{e}", "#FF4136"