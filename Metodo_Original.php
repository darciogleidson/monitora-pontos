public function veiculosRota(Request $request){

if (Cache::has('verificacoes')){
    Cache::increment('verificacoes');
 } else {
    Cache::put('verificacoes', 0, 1000);
 };

$verificacoes = Cache::get('verificacoes');
Cache::put('verificacoes', $verificacoes, 1000);

$inicioConsulta = new DateTime(now());
$versao_rotina = 'Rotina veiculosRota(v3.1)';
//variáveis
//Rotina A
$id_equipamentos_start = "11550,11551,7780,9766,8964,8965,9194,9187,9706,9704,9771,9025,9031,48766,48767,48768,48772,48773,48774,48778,48779,48780";
$id_equipamentos_end = "15701,15717,15626,15624,17888,15646,15640,15722,15668,972,15628,15694,5634,15711,18393";
$intervalo_ponto_start = '10 minutes';
$codigo_municipios = " '09610','93114' ";
$intervalo =  '7 day';
$intervalo_dh_passagem = '60 minutes';
$placas_ignorar = "'JJJ1111','III1110'";
//OBS: a idéia é pegar na dataPassagem os últimos "60 minutos" e desses pegar os últimos "10 minutos" da dataInsercao
//pois não existe index para a dataInsercao, assim diminui o intervalo para o banco fazer scan.

$producao = Input::get('producao','false');
$teste = Input::get('teste','false');

//Mensagem para avisar que o serviço está ativo
if ($verificacoes == 20){
    Cache::put('verificacoes', 0, 1000);
    $mensagem = 'Rotina ' . $versao_rotina . ' Ativa';
    Helper::mensagemTelegram($mensagem,$chatId,$botToken);
}

//Mensagem para avisar que o serviço está ativo
if ($teste <> 'false'){
    $mensagem = "Testando " . $versao_rotina . " - " . $teste;
    Helper::mensagemTelegram($mensagem,$chatId,$botToken);
}

$sql = "select distinct pas_ds_placa from spiabr.tb_pas_passagem pas inner join spiabr.tb_equ_equipamento_fixo equ on pas.equ_id_equipamento_fixo = equ.equ_id_equipamento_fixo
where pas.pas_dh_passagem > (now() - interval '$intervalo')
and equ.equ_id_equipamento_fixo in ($id_equipamentos_start)
and pas.pas_ds_placa in (select distinct pas_ds_placa from spiabr.tb_pas_passagem pas
                            where pas.pas_dh_passagem > (now() - interval '$intervalo_dh_passagem')
                            and pas.pas_ds_placa not in ($placas_ignorar)
                            and pas.equ_id_equipamento_fixo in ($id_equipamentos_end)
                            and pas.pas_dh_insercao > (now() - interval '$intervalo_ponto_start') ) ";
$placas = DB::select(DB::raw($sql));

foreach ($placas as $key => $value) {
    $mensagem = "";
    //Pegar ultima passagem no ponto end
    $sql = "select to_char( pas_dh_passagem , 'yyyy-mm-dd HH24:MI') as pas_dh_passagem, pas.pas_ds_placa, pas.pap_ds_marca_modelo, pas.pap_ds_cor, equ.equ_ds_local_referencia, mun.mun_ds_municipio, mun.uf_sigla
            from spiabr.tb_pas_passagem pas inner join spiabr.tb_equ_equipamento_fixo equ on pas.equ_id_equipamento_fixo = equ.equ_id_equipamento_fixo
                                            inner join spiabr.tb_mun_municipio mun on mun.mun_cd_municipio = equ.mun_cd_municipio
            where pas.pas_dh_passagem > (now() - interval '$intervalo_dh_passagem')
            and pas.equ_id_equipamento_fixo in ($id_equipamentos_end)
            and pas_ds_placa = '$value->pas_ds_placa'
            order by pas_dh_passagem desc
            limit 1";
    $result = DB::select(DB::raw($sql));

    if (isset($result)) {
        $mensagem = $versao_rotina . ' - O veículo ' . $result[0]->pas_ds_placa . ' - ' . $result[0]->pap_ds_marca_modelo . '/' . $result[0]->pap_ds_cor . ' passou em ' . $result[0]->mun_ds_municipio . '/' . $result[0]->uf_sigla . ' - ' . $result[0]-> pas_dh_passagem;
    }

    //Pegar ultima passagem no ponto origem
    $sql = "select to_char( pas_dh_passagem , 'yyyy-mm-dd HH24:MI') as pas_dh_passagem, pas.pas_ds_placa, pas.pap_ds_marca_modelo, pas.pap_ds_cor, equ.equ_ds_local_referencia, mun.mun_ds_municipio, mun.uf_sigla
            from spiabr.tb_pas_passagem pas inner join spiabr.tb_equ_equipamento_fixo equ on pas.equ_id_equipamento_fixo = equ.equ_id_equipamento_fixo
                                            inner join spiabr.tb_mun_municipio mun on mun.mun_cd_municipio = equ.mun_cd_municipio
            where pas.pas_dh_passagem > (now() - interval '$intervalo')
            and equ.equ_id_equipamento_fixo in ($id_equipamentos_start)
            and pas.pas_ds_placa = '$value->pas_ds_placa'
            order by pas_dh_passagem desc
            limit 1";
    $result = DB::select(DB::raw($sql));

    if (isset($result)) {
        $mensagem = $mensagem . ' e também em ' . $result[0]->mun_ds_municipio . '/' . $result[0]->uf_sigla . ' - ' . $result[0]-> pas_dh_passagem;
    }

    Helper::mensagemTelegram($mensagem,$chatId,$botToken);

    if ($producao == 'true'){
        //grupo INTEL 2 - Rotina rotas
        $chatId = "-619122801";
        Helper::mensagemTelegram($mensagem,$chatId,$botToken);
    }

}

//versao 3 (2022/08/03 - Foi adicionado intervalo de pontos para análise de 15 dias)
//Inicio rotina B
//variáveis
$id_equipamentos_start = "3920";
//$id_equipamentos_end = permanece os mesmos
//$intervalo_ponto_start = permanece os mesmos
$intervalo =  '15 day';
//$intervalo_dh_passagem = permanece os mesmos

$chatId = "341387850";
$botToken = "653908071:AAF_HMZlYKzhf31ZCBErB39WNa4p0s0Fvqo";

$sql = "select distinct pas_ds_placa from spiabr.tb_pas_passagem pas inner join spiabr.tb_equ_equipamento_fixo equ on pas.equ_id_equipamento_fixo = equ.equ_id_equipamento_fixo
where pas.pas_dh_passagem > (now() - interval '$intervalo')
and equ.equ_id_equipamento_fixo in ($id_equipamentos_start)
and pas.pas_ds_placa in (select distinct pas_ds_placa from spiabr.tb_pas_passagem pas
                            where pas.pas_dh_passagem > (now() - interval '$intervalo_dh_passagem')
                            and pas.equ_id_equipamento_fixo in ($id_equipamentos_end)
                            and pas.pas_dh_insercao > (now() - interval '$intervalo_ponto_start') ) ";
$placas = DB::select(DB::raw($sql));

foreach ($placas as $key => $value) {
    $mensagem = "";
    //Pegar ultima passagem no ponto end
    $sql = "select to_char( pas_dh_passagem , 'yyyy-mm-dd HH24:MI') as pas_dh_passagem, pas.pas_ds_placa, pas.pap_ds_marca_modelo, pas.pap_ds_cor, equ.equ_ds_local_referencia, mun.mun_ds_municipio, mun.uf_sigla
            from spiabr.tb_pas_passagem pas inner join spiabr.tb_equ_equipamento_fixo equ on pas.equ_id_equipamento_fixo = equ.equ_id_equipamento_fixo
                                            inner join spiabr.tb_mun_municipio mun on mun.mun_cd_municipio = equ.mun_cd_municipio
            where pas.pas_dh_passagem > (now() - interval '$intervalo_dh_passagem')
            and pas.equ_id_equipamento_fixo in ($id_equipamentos_end)
            and pas_ds_placa = '$value->pas_ds_placa'
            order by pas_dh_passagem desc
            limit 1";
    $result = DB::select(DB::raw($sql));

    if (isset($result)) {
        $mensagem = $versao_rotina . ' - O veículo ' . $result[0]->pas_ds_placa . ' - ' . $result[0]->pap_ds_marca_modelo . '/' . $result[0]->pap_ds_cor . ' passou em ' . $result[0]->mun_ds_municipio . '/' . $result[0]->uf_sigla . ' - ' . $result[0]-> pas_dh_passagem;
    }

    //Pegar ultima passagem no ponto origem
    $sql = "select to_char( pas_dh_passagem , 'yyyy-mm-dd HH24:MI') as pas_dh_passagem, pas.pas_ds_placa, pas.pap_ds_marca_modelo, pas.pap_ds_cor, equ.equ_ds_local_referencia, mun.mun_ds_municipio, mun.uf_sigla
            from spiabr.tb_pas_passagem pas inner join spiabr.tb_equ_equipamento_fixo equ on pas.equ_id_equipamento_fixo = equ.equ_id_equipamento_fixo
                                            inner join spiabr.tb_mun_municipio mun on mun.mun_cd_municipio = equ.mun_cd_municipio
            where pas.pas_dh_passagem > (now() - interval '$intervalo')
            and equ.equ_id_equipamento_fixo in ($id_equipamentos_start)
            and pas.pas_ds_placa = '$value->pas_ds_placa'
            order by pas_dh_passagem desc
            limit 1";
    $result = DB::select(DB::raw($sql));

    if (isset($result)) {
        $mensagem = $mensagem . ' e também em ' . $result[0]->mun_ds_municipio . '/' . $result[0]->uf_sigla . ' - ' . $result[0]-> pas_dh_passagem;
    }

    Helper::mensagemTelegram($mensagem,$chatId,$botToken);

    if ($producao == 'true'){
        //grupo INTEL 2 - Rotina rotas
        $chatId = "-619122801";
        Helper::mensagemTelegram($mensagem,$chatId,$botToken);
    }

}
//Fim rotina B

$tempoConsulta = Helper::tempoDeConsulta($inicioConsulta);

if ($tempoConsulta > 30){
    $chatId = "341387850";
    $mensagem = "Tempo de consulta " . $versao_rotina . " = " . $tempoConsulta . "s";
    Helper::mensagemTelegram($mensagem,$chatId,$botToken);
}

$mensagem = 'fim - Tempo consulta ' . $versao_rotina . ' - ' . $inicioConsulta->format('Y-m-d H:i:s') . ' = ' . $tempoConsulta . 's' . ' // verificacoes = ' . $verificacoes;

log::error($mensagem);

return $mensagem;
}
